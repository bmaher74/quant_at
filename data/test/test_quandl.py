import Quandl, os

fname = '%s/.quandl' % os.environ['HOME']
auth = open(fname).read()

df = Quandl.get("CME/CLW2008", 
                trim_start="2008-01-01",
                trim_end="2010-01-01",
                returns="pandas",
                authtoken=auth)

print df
