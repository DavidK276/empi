import * as Sentry from "@sentry/sveltekit";
import { handleErrorWithSentry } from "@sentry/sveltekit";
import { SENTRY_DSN } from '$app/env/public';

Sentry.init({
  dsn: SENTRY_DSN,

  tracesSampleRate: 0.5,

  // Enable logs to be sent to Sentry
  enableLogs: true,



  dataCollection: {
    // To disable sending user data and HTTP bodies, uncomment the lines below. For more info visit:
    // https://docs.sentry.io/platforms/javascript/guides/sveltekit/configuration/options/#dataCollection
    // userInfo: false,
    // httpBodies: [],
  },
});

// If you have a custom error handler, pass it to `handleErrorWithSentry`
export const handleError = handleErrorWithSentry();
