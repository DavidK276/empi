import { createTheme, globalStyle } from '@vanilla-extract/css';

export const [themeClass, vars] = createTheme({
	xs: '0.375rem',
	sm: '0.5rem',
	md: '0.875rem',
	lg: '1rem',
	xl: '2rem',
	xl2: '3rem',
	danger: '#b00020',
	textSecondary: '#fff',
	textPrimary: '#000',
	textTertiary: 'rgb(17 24 39)',
	backgroundPrimary: '#fff',
	backgroundSecondary: 'rgb(17 24 39)',
	link: 'rgb(37 99 235)',
	buttonPrimary: 'rgb(37 99 235)',
	buttonDisabled: 'rgb(128 128 128)'
});

globalStyle('body', {
	fontFamily: '"Source Sans Pro",sans-serif'
});

globalStyle('a', {
	textDecoration: 'none',
	fontWeight: 700,
	margin: `0 ${vars.sm}`,
	color: vars.link,
	display: 'inline-flex',
	alignItems: 'center'
});

globalStyle('button', {
	display: 'inline-flex',
	alignItems: 'center',
	justifyContent: 'center',
	gap: vars.sm,
	borderRadius: vars.xs,
	paddingLeft: vars.md,
	paddingRight: vars.md,
	paddingTop: vars.sm,
	paddingBottom: vars.sm,
	backgroundColor: vars.buttonPrimary,
	color: vars.textSecondary,
	border: 'none',
	whiteSpace: 'nowrap',
	height: 'fit-content'
});

globalStyle('button[disabled]', {
	backgroundColor: vars.buttonDisabled
});

globalStyle('label', {
	display: 'flex',
	color: vars.textTertiary
});

globalStyle('input', {
	display: 'block',
	marginTop: vars.sm,
	width: '100%',
	borderRadius: vars.xs,
	borderWidth: 0,
	padding: `${vars.xs} ${vars.sm}`,
	marginBottom: vars.lg,
	boxShadow: `0 0 2px gray`,
	boxSizing: 'border-box'
});

globalStyle('input[type="text"]', {
	minWidth: '200px'
});

globalStyle('input[type="radio"],input[type="checkbox"]', {
	display: 'inline',
	width: 'initial',
	marginLeft: vars.lg,
	marginBottom: 'initial'
});

globalStyle('select', {
	display: 'block',
	marginTop: vars.sm,
	marginBottom: vars.lg,
	width: '100%',
	borderRadius: vars.xs,
	borderWidth: 0,
	padding: `${vars.xs} ${vars.sm}`,
	boxShadow: `0 0 2px gray`,
	boxSizing: 'border-box'
});

globalStyle('input.error', {
	boxShadow: `0 0 2px red`
});

globalStyle('header', {
	paddingBottom: vars.md
});

globalStyle('footer', {
	marginTop: vars.md,
});

globalStyle('fieldset', {
	margin: `0 0 ${vars.lg} 0`
});