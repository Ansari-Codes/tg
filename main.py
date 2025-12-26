from Routes import *
import ENV

ENV.ui.run(
    host=ENV.HOST, 
    port=ENV.PORT, 
    title=ENV.NAME, 
    favicon=ENV.ICON, 
    storage_secret=ENV.SECRET,
    reload=False,
    on_air=True
)