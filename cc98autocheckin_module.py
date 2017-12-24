from base import DailyNotification_Base
from EasyLogin import EasyLogin
from cc98api import CC98_API_V2

__all__ = ["cc98autocheckin"]

class cc98autocheckin(DailyNotification_Base):
    conf_name = "cc98"
    def work(self):
        assert isinstance(self.conf.accounts,list) # "conf/cc98.py" should contain a list of account, each account (username, password)
        title = "[CC98] "
        content = ""
        for username, password in self.conf.accounts:
            cc98 = CC98_API_V2(username, password)
            oldamount = cc98.get_wealth()
            checkin_status = cc98.signin()
            if not checkin_status:
                continue
            newamount = cc98.get_wealth()
            gained = newamount-oldamount
            title += "{username}: {gained}, ".format(username=username,gained=gained)
            content += "{username}: {newamount}\n\n".format(username=username,newamount=newamount)
        return True, title, content

if __name__ == "__main__":
    cc98autocheckin().run()