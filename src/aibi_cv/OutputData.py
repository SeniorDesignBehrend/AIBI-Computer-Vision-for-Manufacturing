try:
    import pygetwindow as gw
except Exception:
    gw = None

class OutputData:
    __workstation_id: str ## These are private variables
    __output_dir: str     ## Should only be accessed in methods

    def __init__(self, workstation_id: str, output_dir: str):
        self.__workstation_id = workstation_id
        self.__output_dir = output_dir

    def to_exel(self, scanned_data: dict, field_order: list):
        ## Export scanned data to Excel file
        if gw is None:
            return False

        # Export scanned data to Excel file (window automation)
        scanner_windows = [w for w in gw.getAllWindows() if self.__workstation_id in w.title]