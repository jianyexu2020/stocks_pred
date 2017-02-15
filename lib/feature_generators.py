import constants

class FeatureGeneratorBase(object):
    def __init__(self, slicer, history_range, required_cols=None, feature_names=None):
        self.slicer = slicer
        self.history_range = history_range
        self._feature_names = feature_names
        self._required_cols = required_cols

    def required_columns(self):
        required_cols = self._required_cols
        if self.slicer != constants.SLICE_NONE:
            required_cols.append(self.slicer['df_column'])
        return list(set(required_cols))

    def feature_names(self):
        slicer_label = range_label = ""
        if self.slicer != constants.SLICE_NONE:
            slicer_label = "%s_" % self.slicer["label"]
        if self.history_range:
            range_label = "_%ddays" % self.history_range

    def compute_values(self, input_row):
        raise NotImplementedError()

    def init_history_cache(self, db, stock_index):
        raise NotImplementedError()

    def add_to_history_cache(selfself, input_row):
        raise NotImplementedError()

    def remove_from_history_cache(self, input_row):
        raise NotImplementedError()

    def init_on_load(self):
        raise NotImplementedError()

    def slicer_value(self, input_row):
        return input_row[self.slicer["df_column"]]

class ListCacheGeneratorBase(FeatureGeneratorBase):
    def __init__(self, slicer, history_range, required_cols=[], feature_names=[], cache_keys=[]):
        self.cache_key_map = {}
        for i, cache_key in enumerate(cache_keys):
            self.cache_key_map[cache_key] = i
        self.cache = {}
        FeatureGeneratorBase.__init__(self,
                                      slicer,
                                      history_range,
                                      required_cols=required_cols,
                                      feature_names=feature_names)
    def cache_get(self, slicer_value, cache_key, default_value=None):
        if self.cache.get(slicer_value) is None:
            self.cache[slicer_value] = [None] * len(self.cache_key_map)
            slice_cache = self.cache[slicer_value]
            value = slice_cache[self.cache_key_map[cache_key]]
            if value is None:
                return default_value
            return value

    def cache_set(self, slicer_value, cache_key, value):
        if self.cache.get(slicer_value) is None:
            self.cache[slicer_value] = [None] * len(self.cache_key_map)
            slice_cache = self.cache[slicer_value]
            slice_cache[self.cache_key_map[cache_key]] = value

    def init_on_load(self):
        pass


if __name__ == '__main__':
    class StockHistoryGenerator(ListCacheGeneratorBase):
        def __init__(self, slicer, history_range, return_cols=[]):
            self.return_cols = return_cols
            self.history_range= history_range
            self.history_cache = {}
            required_cols = ["Adj_Close", "Date"]
            cache_keys = [
                "avg",
                "count_up",
                "count_down"
            ]
            ListCacheGeneratorBase.__init__(self,
                                            slicer,
                                            history_range,
                                            required_cols=required_cols,
                                            feature_names=return_cols,
                                            cache_keys=cache_keys)

        def compute_values(self, input_row):
            slicer_value = self.slicer_value(input_row)
            history_sum = self.cache_get(slicer_value, "sum", 0.0)
            history_count_up = self.cache_get(slicer_value, "count_up", 0.0)
            history_count_down = self.cache_get(slicer_value, "count_down", 0.0)
            return_values = []
            return_values.append(history_avg,history_count_up, history_count_down)
            return return_values

        def add_to_history_cache(self, input_row):
            slicer_value = self.slicer_value(input_row)
            history_sum = self.cache_get(slicer_value, "sum", 0.0)
            history_count_up = self.cache_get(slicer_value, "count_up", 0.0)
            history_count_down = self.cache_get(slicer_value, "count_down", 0.0)
            self.cache_set(slicer_value, "sum", history_sum+input_row["Adj_Close"])
            self.cache_set(slicer_value, "history_count_up", history_count_up + float(input_row["Adj_Close"]>0))
            self.cache_set(slicer_value, "history_count_down", history_count_down + float(input_row["Adj_Close"]<0))

        def remove_from_history_cache(self, input_row):
            slicer_value = self.slicer_value(input_row)
            history_sum = self.cache_get(slicer_value, "sum", 0.0)
            history_count_up = self.cache_get(slicer_value, "count_up", 0.0)
            history_count_down = self.cache_get(slicer_value, "count_down", 0.0)
            self.cache_set(slicer_value, "sum", history_sum - input_row["Adj_Close"])
            self.cache_set(slicer_value, "history_count_up", history_count_up - float(input_row["Adj_Close"]>0))
            self.cache_set(slicer_value, "history_count_down", history_count_down - float(input_row["Adj_Close"]<0))
