import logging
import threading
import time
from typing import List, Union

from pandas import DataFrame
from tqdm.auto import tqdm

from oscovida import MetadataRegion

from .index import create_markdown_index_page


class ReportExecutor:
    def __init__(
        self,
        *,
        Reporter,
        wwwroot,
        kernel_name="",
        expiry_hours=2,
        attempts=3,
        workers=0,
        force=False,
        verbose=False,
        disable_pbar=False,
        debug=False,
    ) -> None:
        self.Reporter = Reporter
        self.kernel_name = kernel_name
        self.wwwroot = wwwroot
        self.expiry_hours = expiry_hours
        self.attempts = attempts
        self.workers = workers
        self.force = force
        self.verbose = verbose
        self.disable_pbar = disable_pbar
        self.debug = debug

    @property
    def metadata_regions(self) -> DataFrame:
        regions_all = MetadataRegion.get_all_as_dataframe()

        if self.Reporter.category == "all-regions":
            selected_regions = regions_all
        else:
            selected_regions = regions_all[
                regions_all["category"] == self.Reporter.category
            ]

        #  TODO : Not correct as regions actually returns the regions stored in
        #  the metadata, not the regions to be analysed. This should be
        #  clarified later on.
        # if self.debug:
        #     selected_regions = selected_regions[:10]

        return selected_regions

    def _create_html_report_single(
        self, region: Union[List[str], List[List[str]]]
    ) -> None:
        for attempt in range(self.attempts):
            if self.__stop__.is_set():
                raise KeyboardInterrupt

            logging.info(f"Processing {region} attempt {attempt}")
            try:
                report = self.Reporter(
                    region, wwwroot=self.wwwroot, verbose=self.verbose
                )

                recently_generated = (
                    report.metadata.last_updated_hours_ago() < self.expiry_hours
                )
                if recently_generated and not self.force:
                    break

                report.generate(kernel_name=self.kernel_name)
                break  #  Without this break if force is on it will keep attempting
            except Exception as e:
                if e == KeyboardInterrupt:
                    raise e

                if attempt + 1 == self.attempts:
                    logging.warning(f"Processing {region} error\n{e}")
                    raise e

                logging.warning(
                    f"Processing {region} error {type(e)}, retrying {attempt+1}"
                )

    def _create_html_reports_serial(
        self, regions: Union[List[str], List[List[str]]]
    ) -> None:
        #  If the progress bar is disabled then pbar is set to a normal range
        #  instead of the tqdm bar object
        if self.disable_pbar:
            pbar = range(len(regions))
        else:
            pbar = tqdm(range(len(regions)))

        try:
            for i in pbar:
                #  Regions can be a list of strings, or in the case of an area
                #  with subregions it is a list of lists. The last element of
                #  the list is the smallest/most specific region, so that is
                #  used for the region string. e.g. for Germany the regions
                #  are [Bundesland, Kreis], so the Kreis is the region_str
                region = regions[i]
                region_str = region[-1] if type(region) == list else region
                if self.disable_pbar:
                    logging.info(f"Processing {region_str}")
                else:
                    pbar.set_description(f"Processing {region_str}")

                self._create_html_report_single(region)
        except KeyboardInterrupt:
            logging.warning(f"stopped {KeyboardInterrupt}")

    def _create_html_reports_parallel(
        self, regions: Union[List[str], List[List[str]]]
    ) -> None:
        self.__stop__ = threading.Event()

        padding = self.workers - (len(regions) % self.workers)
        regions = regions + ([None] * padding)
        per_worker = int(len(regions) / self.workers)

        #  Weird way to create an evenly distributed list
        regions_per_worker = [[] for p in range(self.workers)]
        [
            regions_per_worker[w].append(r)
            for w, r in zip(list(range(self.workers)) * per_worker, regions)
        ]
        regions_per_worker = [
            list(filter(None.__ne__, worker)) for worker in regions_per_worker
        ]
        regions_per_worker = list(filter(None, regions_per_worker))

        self.threads = []

        print(f"Using {self.workers} workers with tasks:")
        for n in range(len(regions_per_worker)):
            thread_name = f"OscovidaWorker {n}"
            if len(regions_per_worker[n]) > 5:
                print(f"\t{thread_name}: {len(regions_per_worker[n])} regions...")
            else:
                print(f"\t{thread_name}: {regions_per_worker[n]}")

            t = threading.Thread(
                target=self._create_html_reports_serial,
                args=(tuple(regions_per_worker[n]),),
                name=thread_name,
            )

            self.threads.append(t)
        print("")

        [t.start() for t in self.threads]

        return None

    def create_html_reports(
        self, regions: Union[List[str], List[List[str]]]
    ) -> None:
        if self.workers:
            #  Works with both ThreadPoolExecutor and ProcessPoolExecutor
            #  for this task multithreading and multiprocessing perform
            #  about the same
            self._create_html_reports_parallel(regions)
            while any([thread.is_alive() for thread in self.threads]):
                try:
                    #  running `while True` while doing nothing seems bad
                    time.sleep(0.5)
                except KeyboardInterrupt:
                    self.__stop__.set()
                    logging.warning(f"stopped")
        else:
            self._create_html_reports_serial(regions)

    def create_markdown_index_page(
        self,
        save_as: str = None,
        slug: str = None,
        pelican_file_path: str = None,
        title_prefix: str = "Tracking plots: ",
    ) -> None:
        create_markdown_index_page(
            self.metadata_regions,
            self.Reporter.category,
            save_as,
            slug,
            pelican_file_path,
            title_prefix,
        )
