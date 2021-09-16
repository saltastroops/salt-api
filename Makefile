cypress: ## launch the Cypress test runner
	npx cypress open

end2end: ## run end-to-end tests
	npx cypress run

mkdocs: ## start development documentation server
	mkdocs serve

prettier: ## format JavaScript code
	npx prettier --write .

prettier-staged: ## format staged JavaScript files
	npm run pretty-quick:staged

test: ## run various tests (but no end-to-end tests)
	npx prettier --check cypress
	npx cypress run
