"""
Vocabulary & VocabularyBank — 單字模型 (Vocabulary Model)

Vocabulary  : 單一單字的資料結構 (Data Structure)。
VocabularyBank : 管理所有課別單字的集合，負責從 CSV 載入資料。
"""

import csv
import os
import glob


class Vocabulary:
    """代表一個日文單字的類別 (Class)。"""

    def __init__(self, japanese: str, reading: str, chinese: str, unit: int):
        self.japanese = japanese
        self.reading = reading
        self.chinese = chinese
        self.unit = unit

    def as_tuple(self) -> tuple:
        """回傳 tuple 格式：(japanese, reading, chinese, unit)。"""
        return (self.japanese, self.reading, self.chinese, self.unit)

    def __repr__(self) -> str:
        return (f"Vocabulary(japanese='{self.japanese}', "
                f"reading='{self.reading}', "
                f"chinese='{self.chinese}', unit={self.unit})")


class VocabularyBank:
    """
    管理所有課別單字的類別 (Class)。

    內部使用 dict (字典) 以課別編號為鍵 (Key) 儲存單字列表 (List)。
    """

    def __init__(self):
        self._units: dict[int, list[Vocabulary]] = {}

    def load_from_csv(self, filepath: str, unit_id: int,
                      encoding: str = "utf-8"):
        """
        從 CSV 檔案載入單字。

        CSV 欄位 (Column) 順序：japanese, reading, chinese

        Parameters:
            filepath — CSV 檔案路徑 (File Path)
            unit_id  — 課別編號
            encoding — 檔案編碼，預設 utf-8

        Raises:
            FileNotFoundError — 檔案不存在時拋出
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"找不到單字檔案：{filepath}")

        vocabs = []
        try:
            with open(filepath, "r", encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        v = Vocabulary(
                            japanese=row["japanese"].strip(),
                            reading=row["reading"].strip(),
                            chinese=row["chinese"].strip(),
                            unit=unit_id,
                        )
                        vocabs.append(v)
                    except (KeyError, ValueError) as e:
                        # 跳過格式錯誤的列 (Row)，繼續載入其餘資料
                        print(f"[警告] 第 {reader.line_num} 列格式錯誤，已跳過：{e}")
        except csv.Error as e:
            print(f"[警告] CSV 檔案讀取錯誤：{e}")

        self._units[unit_id] = vocabs

    def load_all_from_directory(self, data_dir: str,
                                encoding: str = "utf-8"):
        """
        自動掃描 data 目錄 (Directory) 中所有 vocab_unitXX.csv 並載入。

        檔名格式：vocab_unit01.csv, vocab_unit02.csv, ...
        """
        pattern = os.path.join(data_dir, "vocab_unit*.csv")
        files = sorted(glob.glob(pattern))

        if not files:
            raise FileNotFoundError(
                f"在 {data_dir} 中找不到任何 vocab_unit*.csv 檔案。"
            )

        for filepath in files:
            # 從檔名擷取課別編號，例如 vocab_unit01.csv → 1
            basename = os.path.basename(filepath)
            try:
                unit_str = basename.replace("vocab_unit", "").replace(".csv", "")
                unit_id = int(unit_str)
            except ValueError:
                print(f"[警告] 無法辨識課別編號：{basename}，已跳過。")
                continue

            self.load_from_csv(filepath, unit_id, encoding)

    def get_unit(self, unit_id: int) -> list:
        """取得特定課別的單字列表 (List)。"""
        return self._units.get(unit_id, [])

    def get_all(self) -> list:
        """取得所有課別的單字列表 (List)。"""
        all_vocabs = []
        for vocabs in self._units.values():
            all_vocabs.extend(vocabs)
        return all_vocabs

    def get_unit_ids(self) -> list:
        """取得所有已載入的課別編號，排序後回傳。"""
        return sorted(self._units.keys())

    def get_unit_count(self) -> int:
        """取得已載入的課別數量。"""
        return len(self._units)
