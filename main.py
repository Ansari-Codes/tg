from Routes import *
import ENV
import app_endpoints

ENV.ui.run(
    host=ENV.HOST, 
    port=ENV.PORT, 
    title=ENV.NAME, 
    favicon=ENV.ICON, 
    storage_secret=ENV.SECRET
)