import luigi
from stocks.daily_update import daily_update_stocks
from stocks.build_features import build_features

class DailyUpdate(luigi.Task):
    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget("stocks.csv")

    def run(self):
        stocks_data = daily_update_stocks()
        stocks_data.to_csv("stocks.csv")

class BuildFeatures(luigi.Task):
    def requires(self):
        return [DailyUpdate()]

    def output(self):
        return luigi.LocalTarget("report_today.csv")

    def run(self):
        report_today = build_features()
        report_today.to_csv("report_today.csv")


if __name__ == "__main__":
    luigi.run()