.PHONY: all report clean

all: report

report:
	$(MAKE) -C reports pdf

clean:
	$(MAKE) -C reports clean
