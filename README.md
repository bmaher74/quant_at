# Python Code for Algorithmic Trading

This project is a collection of Python codes that aim to replicate the
Matlab codes for Dr. Ernest Chan's book *Algorithmic Trading*.

The file names for scripts reflect Dr. Chan's Matlab script names, for
example the code for `Ratio.m` is in `Ratio.py`.

All feedback, comments, pull requests are welcome. 

## Requirements

Run `pip install` on

```
numpy
scipy
statsmodels
pandas
arch
```

There are three big data files that are hard to share through Github,
they can be downloaded through the links below:

[AUDCAD](https://dl.dropboxusercontent.com/u/1570604/data/inputData_AUDCAD_20120426.mat)

[AUDUSD](https://dl.dropboxusercontent.com/u/1570604/data/inputData_AUDUSD_20120426.mat)

[USDCAD](https://dl.dropboxusercontent.com/u/1570604/data/inputData_USDCAD_20120426.mat)

The code will assume these files are under `[HOME]/Dropbox/Public/data` folder.

## Converting MAT Files to CSV

I prefer to work with CSV files, the Pandas library makes it a breeze
to access them plus I can view the contents of CSV files easily,
manipulate them with Unix based tools if necessary, etc. For
converting any of mat files into csv, this is the method I followed:
1) Find the Matlab script from Dr. Chan's book that reads and prepares
the data, i.e. `TU_mom.m` 2) find the point where the data is all
ready, i.e.

```
clear;
load('inputDataOHLCDaily_20120511', 'syms', 'tday', 'cl');
..
idx=strmatch('TU', syms, 'exact');
tday=tday(:, idx);
cl=cl(:, idx);
..
```

3) After the last line above, the `tday,cl` variables are all ready,
with the same dimensions, etc. We can create a data matrix out of
these and write them to disk. 4) Insert the following in the script,

```
A = [tday cl];
save('/tmp/out','A');
exit;
```

and run it. 5) Now from a seperate Python script,

```
from scipy import io as spio
import numpy as np
import pandas as pd

y = spio.loadmat('/tmp/out.mat')['A']
df = pd.DataFrame(y, columns=['Date','Close'])
df.to_csv('/tmp/out.csv',index=None)
```

This gives you a CSV file.

## LINKS

[Ernie Chan's Blog](http://epchan.blogspot.com)

[Algorithmic Trading] (http://amzn.to/1F4RTtT) (Book)

[My Blog] (http://sayilarvekuramlar.blogspot.com)

## LICENSE

The code is licensed under GPL v3. See COPYING for details.
