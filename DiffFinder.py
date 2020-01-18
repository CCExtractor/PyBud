import dictdiffer


class DiffFinder:
    def __init__(self):
        self.changes = []
        self.var_name = None

    def evaluate_diff(self, var_name, old, new) -> (bool, list):
        diff = list(dictdiffer.diff(old, new))
        if len(diff) == 0:  # variable did not change in any way
            return False, None
        self.changes = []  # reset changes store
        self.var_name = var_name
        # for each difference found, do:
        for diff_type, change_path, difference in diff:
            if diff_type == dictdiffer.ADD:
                self.var_add(change_path, difference)
            elif diff_type == dictdiffer.CHANGE:
                self.var_change(change_path, difference)
            elif diff_type == dictdiffer.REMOVE:
                self.var_remove(change_path, difference)
        # print(self.changes)  # DEBUG
        return True, self.changes

    def var_add(self, change_path, chg):
        temp_event = {"type": "add", "var_name": self.var_name, "var_path": ""}
        # there is a internal path within the variable to reference the addition, thus the variable has sub-elements
        if len(change_path) != 0:
            temp_event["var_path"] = change_path  # log path to addition
            for key, val in chg:
                # log values to event
                temp_event["element"] = key
                temp_event["new_val"] = val
                # print("var add if")  # DEBUG
                self.changes.append(temp_event)  # log event to changes
        # else the change is a list of variable name and value pairs
        else:
            for path, val in chg:
                # log values to event
                temp_event["element"] = path
                temp_event["new_val"] = val
                # print("var add else")  # DEBUG
                self.changes.append(temp_event)  # log event to changes

    def var_change(self, change_path, chg):
        old, new = chg
        temp_event = {"type": "change", "var_name": self.var_name, "var_path": ""}

        # changed path is formatted as list, variable has sub-elements
        if isinstance(change_path, list):
            temp_event["var_path"] = change_path.copy()  # log path to change
        elif len(change_path) != 0 and isinstance(change_path, str):  # else check if the path exists and is a string
            temp = change_path.split(".")  # deep copy causes this to sometimes be in form: "item1.item2", delimit
            temp_event["var_path"] = temp  # log path to change
        # log values to event
        temp_event["old_val"] = old
        temp_event["new_val"] = new
        # print("var change")  # DEBUG
        self.changes.append(temp_event)  # log event to changes

    def var_remove(self, change_path, chg, ):
        temp_event = {"type": "remove", "var_name": self.var_name, "var_path": ""}
        # there is a internal path within the variable to reference the addition, thus the variable has sub-elements
        if len(change_path) != 0:
            temp_event["var_path"] = change_path  # log path to addition
            for key, val in chg:
                # log values to event
                temp_event["element"] = key
                temp_event["old_val"] = val
                # print("var remove if")  # DEBUG
                self.changes.append(temp_event)  # log event to changes
        # else the change is a list of variable name and value pairs
        else:
            for path, val in chg:
                # log values to event
                temp_event["element"] = path
                temp_event["old_val"] = val
                # print("var remove else")  # DEBUG
                self.changes.append(temp_event)  # log event to changes
