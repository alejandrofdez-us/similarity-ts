class SimilarityAnalysisComputer:
    def __init__(self, similarity_ts, analysis):
        self.ts1_ts2_associated_windows_iterator = iter(similarity_ts.ts1_ts2_associated_windows.items())
        self.similarity_ts = similarity_ts
        self.analysis = analysis
        self.analysis_iterator = iter(analysis)
        self.length = len(analysis) * len(similarity_ts.ts1_ts2_associated_windows.items())
        self.current_associated_window = None

    def __iter__(self):
        self.current_associated_window = next(self.ts1_ts2_associated_windows_iterator)
        return self

    def __next__(self):
        try:
            return self._compute_next_analysis()
        except StopIteration:
            self.current_associated_window = next(self.ts1_ts2_associated_windows_iterator)
            self.analysis_iterator = iter(self.analysis)
            return self._compute_next_analysis()

    def __len__(self):
        return self.length

    def _compute_next_analysis(self):
        raise NotImplementedError('Subclasses must implement _compute_next_analysis() method')
