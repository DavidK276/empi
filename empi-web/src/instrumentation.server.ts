import * as Sentry from '@sentry/sveltekit';

Sentry.init({
  dsn: 'https://e8c9845228f84231bc4801f9935daf23@glitchtip.znamafirma.xyz/2',

  tracesSampleRate: 1.0,

  // Enable logs to be sent to Sentry
  enableLogs: true,

  // uncomment the line below to enable Spotlight (https://spotlightjs.com)
  // spotlight: import.meta.env.DEV,
});