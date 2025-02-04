.ONESHELL: 

ENV :=land-cover-explorer
PY_VERSION :=3.8

CONDA_CREATE_OPS := --file=environment.yml --name $(ENV) --yes

PROJECT_NAME :=Land_Cover_Explorer
POETRY_DEPS := geopandas matplotlib rasterio
POETRY_OPS := --no-interaction

POETRY_INIT := poetry init $(POETRY_OPS)

all: install_dependencies
	@echo ">>> Done"

install_dependencies: add_dependencies
	@echo ">>> Installing dependencies"
	conda run -n $(ENV) poetry install --no-root

add_dependencies: configure_environment
	@echo ">>> Adding dependencies"
	conda run -n $(ENV) poetry add $(POETRY_DEPS)

configure_environment: create_environment 
ifeq (,$(shell dir /b | findstr pyproject.toml))
	@echo ">>> No Poetry project found, Initializing" 
	conda run -n $(ENV) $(POETRY_INIT)
else
	@echo ">>> Poetry project already exists"
endif

create_environment:
ifeq (,$(shell conda env list | findstr $(ENV)))
	@echo ">>> Creating conda environment $(ENV)"
	conda env create $(CONDA_CREATE_OPS)
else
	@echo ">>> Conda environment $(ENV) already exists"
endif

