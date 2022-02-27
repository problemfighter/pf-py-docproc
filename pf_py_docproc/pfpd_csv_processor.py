import csv
from abc import ABC, abstractmethod
from pf_py_common.pf_exception import PFException
from pf_py_file.pfpf_file_util import PFPFFileUtil


class CSVCustomProces(ABC):

    @abstractmethod
    def process(self, csv_cols, obj):
        pass


class PFPDCSVProcessor:

    def file_to_csv_obj(self, file_path, delimiter=','):
        if not PFPFFileUtil.is_exist(file_path):
            raise PFException("Invalid CSV File")
        with open(file_path) as csv_file:
            return csv.reader(csv_file, delimiter=delimiter)

    def _is_index_exist(self, data: list, index):
        try:
            value = data[index]
            return True
        except IndexError:
            return False

    def csv_to_dict_list(self, file_path, key_mapping: list, delimiter=',', custom_proces: CSVCustomProces = None):
        return self._csv_to_mapping(file_path, key_mapping, None, delimiter, custom_proces)

    def csv_to_object(self, file_path, key_mapping: list, object_class, delimiter=',', custom_proces: CSVCustomProces = None):
        return self._csv_to_mapping(file_path, key_mapping, object_class, delimiter, custom_proces)

    def _csv_to_mapping(self, file_path, key_mapping: list, object_class=None, delimiter=',', custom_proces: CSVCustomProces = None):
        if not PFPFFileUtil.is_exist(file_path):
            raise PFException("Invalid CSV File")

        definition_list = []
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            for cols in csv_reader:
                obj = self._csv_map_by_key_mapper(cols, key_mapping, object_class, custom_proces)
                if obj:
                    definition_list.append(obj)
        return definition_list

    def _csv_map_by_key_mapper(self, csv_cols, key_mapping: list, object_class=None, custom_proces: CSVCustomProces = None):
        if not key_mapping:
            return csv_cols
        obj = {}
        if object_class:
            obj = object_class()
        for index, key in enumerate(key_mapping):
            if key and self._is_index_exist(csv_cols, index):
                if isinstance(obj, dict):
                    obj[key] = csv_cols[index]
                elif hasattr(obj, key):
                    setattr(obj, key, csv_cols[index])
        if custom_proces:
            obj = custom_proces.process(csv_cols, obj)
        return obj


pfpd_csv_processor = PFPDCSVProcessor()
