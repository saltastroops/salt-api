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
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      const usernames = require(process.env["TEST_DATA_DIR"] +
        "/e2e/usernames.json");
      for (const key in { ...usernames }) {
        config.env[key] = usernames[key];
      }

      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      require("cypress-grep/src/plugin")(config);

      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      require("./cypress/plugins/index.ts").default(on, config);
      return config;
    },
    baseUrl: "http://127.0.0.1:4200",
  },
});
