import Motio.UI.ViewModels.GraphicsAffectingNodeViewModel as BaseClass
from Motio.UI.Utils import ProxyStatic

class ColorViewModel(BaseClass):
    def __new__(cls, *args):
        instance = BaseClass.__new__(cls, *args)
        instance.Original.Properties["type"].PropertyChanged += instance.onDropDownChanged
        return instance

    def get_UserGivenName(self):
        return "custom name in the ui layer"

    def onDropDownChanged(self,sender,args):
        if args.PropertyName == "StaticValue":
            self.getProperty("type").Visible = False

    def getProperty(self, name):
        return ProxyStatic.GetProxyOf(self.Original.Properties[name])