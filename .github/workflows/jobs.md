Trigger: PR, PUSH
- job 1:
	get the non-EOL versions list from the get_nonEOL_Python.py script and build the versions test matrix
- job 2:
	run pytest on each version
