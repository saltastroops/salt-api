import { defineConfig } from "cypress";

export default defineConfig({
  video: false,
  defaultCommandTimeout: 15000,
  retries: {
    runMode: 4,
    openMode: 0,
  },
  e2e: {
    // We've imported your old cypress plugins here.
    // You may want to clean this up later by importing these.
    setupNodeEvents(on, config) {
      return require("./cypress/plugins/index.ts").default(on, config);
    },
    baseUrl: "http://127.0.0.1:4200",
  },
});
