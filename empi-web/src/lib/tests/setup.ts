import '@testing-library/svelte/vitest';
import { loadTranslations } from '../translations';

const initLocale = 'sk';

await loadTranslations(initLocale, '/');