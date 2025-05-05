from concurrent.futures import ThreadPoolExecutor


class DataProcessor():
    def __init__(self, data, data_processor, max_workers = 3):
        self.data = data
        self.data_processor = data_processor
        self.max_workers = max_workers
    
    def __process_wrapper(self, d):
        if isinstance(d, dict):
            return self.data_processor(**d)
        else:
            return self.data_processor(d)

    def run_concurrently(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(self.__process_wrapper, self.data))
        return results