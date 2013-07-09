#!/usr/bin/python
import inmeth
import web
            
if __name__=="__main__":
    web.internalerror = web.debugerror
    inmeth.app.run()
