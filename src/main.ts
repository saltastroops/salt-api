import { enableProdMode } from "@angular/core";
import { platformBrowserDynamic } from "@angular/platform-browser-dynamic";

import * as Sentry from "@sentry/angular";
import { Integrations } from "@sentry/tracing";

import { AppModule } from "./app/app.module";
import { environment } from "./environments/environment";

if (environment.sentryDSN) {
  Sentry.init({
    dsn: environment.sentryDSN,
    integrations: [
      new Integrations.BrowserTracing({
        tracingOrigins: ["localhost", environment.apiUrl],
        routingInstrumentation: Sentry.routingInstrumentation,
      }),
    ],

    // Set tracesSampleRate to 1.0 to capture 100%
    // of transactions for performance monitoring.
    // We recommend adjusting this value in production
    tracesSampleRate: environment.sentryTracesSampleRate,
  });
} else {
  console.warn("SENTRY_DSN variable is not set.");
}

if (environment.production) {
  enableProdMode();
}

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .catch((err) => console.error(err));
