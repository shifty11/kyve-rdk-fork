
# Get all modules by looking for subfolders with a Makefile (excluding node_modules)
MODULES := $(shell find . -mindepth 2 -maxdepth 4 -name Makefile -exec dirname {} \; | grep -v "node_modules")
RESULT_FILE := /tmp/kyvejs-result
GO_VERSION := $(shell go version | cut -c 14- | cut -d' ' -f1 | cut -d'.' -f1,2)

###############################################################################
###                                 Checks                                  ###
###############################################################################

ensure_all: ensure_go_version ensure_yarn

# Check if specified go version is installed
ensure_go_version:
ifneq ($(GO_VERSION),1.22)
	$(error ❌  Please run Go v1.22.x..)
endif

# Check if yarn is installed
ensure_yarn:
	@yarn --version > /dev/null 2>&1 || (echo "❌ Yarn not found.\n- Is yarn installed?\n- Did you forget to execute \`nvm use\`?" && exit 1)

###############################################################################
###                          Formatting & Linting                           ###
###############################################################################

gofumpt_cmd=mvdan.cc/gofumpt
golangci_lint_cmd=github.com/golangci/golangci-lint/cmd/golangci-lint

# loop through all modules and run the format command (in parallel)
format: ensure_all
	@rm -f $(RESULT_FILE)
	@set -e; for module in $(MODULES); do \
	  if make -C $$module -n format > /dev/null 2>&1; then \
	   { $(MAKE) $$module.format || echo $$? > $(RESULT_FILE); } & \
	  fi; \
 	done; wait; if [ -f $(RESULT_FILE) ]; then exit `cat $(RESULT_FILE)`; fi

%.format:
	@$(MAKE) -C $* format

# loop through all modules and run the lint command (in parallel)
lint: ensure_all
	@rm -f $(RESULT_FILE)
	@set -e; for module in $(MODULES); do \
	  if make -C $$module -n lint > /dev/null 2>&1; then \
		{ $(MAKE) $$module.lint || echo $$? > $(RESULT_FILE); } & \
	  fi; \
	done; wait; if [ -f $(RESULT_FILE) ]; then exit `cat $(RESULT_FILE)`; fi

%.lint:
	@$(MAKE) -C $* lint

###############################################################################
###    		                       Protobuf    		                        ###
###############################################################################

proto-gen:
	sh ./common/proto/proto-gen.sh

###############################################################################
###    		                       Kystrap    		                        ###
###############################################################################

# Run kystrap to create a new runtime
# Usage: make bootstrap-runtime ARGS="--name my-runtime -language go"
bootstrap-runtime:
	sh ./tools/kystrap/kystrap.sh create $(ARGS)

test-runtime:
	sh ./tools/kystrap/kystrap.sh test $(ARGS)

###############################################################################
### 						 	   Testing									###
###############################################################################

# Runs the e2e tests in a local environment
test-e2e: ensure_go_version
	@cd test/e2e && make test

# Runs the e2e tests in a dind container (docker in docker)
# This is useful for running tests in a CI environment or for local testing
test-e2e-dind:
	@echo "🧪 Running end-to-end tests (dind)..."
	@./test/e2e/run-e2e-tests.sh
	@echo "✅ Completed end-to-end tests (dind)!"

###############################################################################
### 							 	Docker 							 		###
###############################################################################

# Builds the docker image for all modules (in parallel)
build-docker-images:
	@rm -f $(RESULT_FILE)
	@set -e; for module in $(MODULES); do \
	  if make -C $$module -n docker-image > /dev/null 2>&1; then \
		{ $(MAKE) $$module.build-docker-image || echo $$? > $(RESULT_FILE); } & \
	  fi; \
	done; wait; if [ -f $(RESULT_FILE) ]; then exit `cat $(RESULT_FILE)`; fi

%.build-docker-image:
	@$(MAKE) -C $* docker-image
