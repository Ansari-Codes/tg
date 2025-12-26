from Routes import *
import ENV

ENV.ui.run(
    host=ENV.HOST, 
    port=8080, 
    title=ENV.NAME, 
    favicon=ENV.ICON, 
    storage_secret=ENV.SECRET,
    reload=True,
    on_air=True
)