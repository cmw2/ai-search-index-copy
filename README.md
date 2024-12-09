A simple python script to copy document entries from one AI Search index to another.  

It uses top/skip to copy in batches, however this may not work if subsequent search calls return documents in a different order.  This is an area to be researched/refined.

You'll need python and to install the azure-search-documents and azure-identity packages.
