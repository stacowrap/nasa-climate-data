
default: clean_derived collate wrangle publish

# by default, we don't attempt to fetch new data
stash:
	./src/stash_data.sh

collate:
	./src/collate_data.py

wrangle:
	./src/wrangle_data.py

publish:
	./src/publish_viz.py

### CLEANING/DELETION STUFF
clean: clean_derived


clean_all: clean_stashed clean_derived

clean_derived:
	rm -rf data/collated data/wrangled data/published

clean_stashed:
	rm -rf data/stashed
