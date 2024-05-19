import { createTheme } from '@vanilla-extract/css';

export const [themeClass, vars] = createTheme({
	xs: 'var(--xs)',
	sm: 'var(--sm)',
	md: 'var(--md)',
	lg: 'var(--lg)',
	xl: 'var(--xl)',
	xl2: 'var(--2xl)',
	danger: 'var(--danger)',
	textSecondary: 'var(--text-secondary)',
	textPrimary: 'var(--text-primary)',
	backgroundPrimary: 'var(--background-primary)',
	backgroundSecondary: 'var(--background-secondary)',
	backgroundCritical: 'var(--background-critical)',
	link: 'var(--link)',
	buttonPrimary: 'var(--button-primary)',
	buttonDisabled: 'var(--button-disabled)',
	success: 'var(--success)'
});