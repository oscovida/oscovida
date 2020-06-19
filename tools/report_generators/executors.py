import logging
import threading
import time

from coronavirus import MetadataRegion
from tqdm.notebook import trange

# logging.basicConfig(
#     format="%(asctime)s %(threadName)s: %(message)s",
#     level=logging.DEBUG,
#     datefmt="%H:%M:%S"
# )


class ReportExecutor:
    def __init__(self, *,
        Reporter, wwwroot, expiry_hours=2, attempts=3, workers=0,
        force=False, verbose=False
    ) -> None:
        self.Reporter = Reporter
        self.wwwroot = wwwroot
        self.expiry_hours = expiry_hours
        self.attempts = attempts
        self.workers = workers
        self.force = force
        self.verbose = verbose

    @property
    def regions(self):
        regions_all = MetadataRegion.get_all_as_dataframe()
        return regions_all[regions_all['category'] == self.Reporter.category]

    def _create_html_report_single(self, region) -> None:
        for attempt in range(self.attempts):
            if self.__stop__.is_set():
                raise KeyboardInterrupt

            logging.debug(f"Processing {region} attempt {attempt}")
            try:
                report = self.Reporter(region, wwwroot=self.wwwroot, verbose=self.verbose)
                recently_generated = report.metadata.last_updated_hours_ago() < self.expiry_hours
                if recently_generated and not self.force:
                    break

                report.generate()
                break #  Without this break if force is on it will keep attempting
            except Exception as e:
                if e == KeyboardInterrupt:
                    raise e

                if attempt + 1 == self.attempts:
                    logging.warning(f"Processing {region} error\n{e}")
                    raise e

                logging.warning(f"Processing {region} error {type(e)}, "
                                f"retrying {attempt+1}")

    def _create_html_reports_serial(self, regions):
        pbar = trange(len(regions))
        try:
            for i in pbar:
                region = regions[i]
                region_str = region[-1] if type(region) == list else region
                pbar.set_description(f"Processing {region_str}")

                self._create_html_report_single(region)
        except KeyboardInterrupt:
            logging.warning(f"stopped {KeyboardInterrupt}")

    def _create_html_reports_parallel(self, regions):
        self.__stop__ = threading.Event()

        padding = self.workers - (len(regions) % self.workers)
        regions = regions + ([None] * padding)
        per_worker = int(len(regions) / self.workers)

        #  Weird way to create an evenly distributed list
        regions_per_worker = [[] for p in range(self.workers)]
        [
            regions_per_worker[w].append(r)
            for w, r
            in zip(list(range(self.workers)) * per_worker, regions)
        ]
        regions_per_worker = [
            list(filter(None.__ne__, worker))
            for worker
            in regions_per_worker
        ]
        regions_per_worker = list(filter(None, regions_per_worker))

        self.threads = []

        print(f"Using {self.workers} workers with tasks:")
        for n in range(self.workers):
            thread_name = f"OscovidaWorker {n}"
            if len(regions_per_worker[n]) > 5:
                print(f"\t{thread_name}: {len(regions_per_worker[n])} regions...")
            else:
                print(f"\t{thread_name}: {regions_per_worker[n]}")

            t = threading.Thread(
                target=self._create_html_reports_serial,
                args=(tuple(regions_per_worker[n]),),
                name=thread_name
            )

            self.threads.append(t)
        print("")

        [t.start() for t in self.threads]

    def create_html_reports(self, regions):
        if self.workers:
            #  Works with both ThreadPoolExecutor and ProcessPoolExecutor
            #  for this task multithreading and multiprocessing perform
            #  about the same
            self._create_html_reports_parallel(regions)
            while any([thread.is_alive() for thread in self.threads]):
                try:
                    time.sleep(0.5)
                except KeyboardInterrupt:
                    self.__stop__.set()
                    logging.warning(f"stopped")
        else:
            self._create_html_reports_serial(regions)
