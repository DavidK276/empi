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
	backgroundPrimary: '#fff'
});