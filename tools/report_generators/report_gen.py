from tqdm.notebook import trange, tqdm
from concurrent.futures import ThreadPoolExecutor


class ReportExecutor:
    def __init__(self, *,
        Reporter, wwwroot, expiry_hours=2, attempts=3, workers=None,
        force=False, verbose=False
    ) -> None:
        self.__shutdown__ = False
        self.Reporter = Reporter
        self.wwwroot = wwwroot
        self.expiry_hours = expiry_hours
        self.attempts = attempts
        self.workers = workers
        self.force = force
        self.verbose = verbose

    def create_html_report_single(self, region) -> None:
        for attempt in range(self.attempts):
            if self.__shutdown__:
                raise KeyboardInterrupt
            try:
                report = self.Reporter(region, wwwroot=self.wwwroot, verbose=self.verbose)
                if report.metadata.last_updated_hours_ago() < self.expiry_hours and not self.force:
                    continue
                report.generate()
            except Exception as e:
                if e == KeyboardInterrupt:
                    raise e
                if attempt + 1 == self.attempts:
                    print(f"Error for {region}")
                    print(e)
                    raise e
            else:
                break

    def create_html_reports_serial(self, regions):
        pbar = trange(len(regions))
        for i in pbar:
            region = regions[i]
            region_str = region[-1] if type(region) == list else region
            pbar.set_description(f"Processing {region_str}")

            self.create_html_report_single(region)

    def create_html_reports_parallel(self, regions, pool):
        if not self.workers:
            raise Exception

        padding = self.workers - (len(regions) % self.workers)
        regions = regions + ([None] * padding)
        per_worker = int(len(regions) / self.workers)
        #  Weird way to create an evenly distributed list
        regions_per_worker = [[] for p in range(self.workers)]
        [
            regions_per_worker[w].append(r)
            for w, r in list(zip(list(range(self.workers)) * per_worker, regions))
        ]
        regions_per_worker = [
            list(filter(None.__ne__, worker)) for worker in regions_per_worker
        ]

        print(f"Using {self.workers} workers with tasks:")
        for n in range(self.workers):
            if len(regions_per_worker[n]) > 5:
                print(f"\t{n}: {len(regions_per_worker[n])} regions...")
            else:
                print(f"\t{n}: {regions_per_worker[n]}")
        print("")


        pool.map(self.create_html_reports_serial, regions_per_worker)

    def create_html_reports(self, regions):
        if self.workers:
            #  Works with both ThreadPoolExecutor and ProcessPoolExecutor
            #  for this task multithreading and multiprocessing perform
            #  about the same
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                try:
                    self.create_html_reports_parallel(regions, pool)
                except Exception as e:
                    print("SHUTDOWN")
                    self.__shutdown__ = True
                    raise e
        else:
            self.create_html_reports_serial(regions)
