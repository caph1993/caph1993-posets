rm ./dist/*
python3 setup.py check && python3 setup.py sdist && twine upload dist/* && pip3 install --upgrade caph1993-posets && pip3 install --upgrade caph1993-posets
