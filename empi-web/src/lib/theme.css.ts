import { createTheme } from '@vanilla-extract/css';

export const [themeClass, vars] = createTheme({
	xs: '0.375rem',
	sm: '0.5rem',
	md: '0.875rem',
	lg: '1rem',
	xl: '2rem',
	xl2: '3rem',
	textSecondary: '#fff',
	textPrimary: '#000',
	textTertiary: 'rgb(17 24 39)',
	backgroundPrimary: '#fff',
	backgroundSecondary: 'rgb(17 24 39)',
	link: 'rgb(37 99 235)',
	buttonPrimary: 'rgb(37 99 235)',
	buttonDisabled: 'rgb(128 128 128)'
});