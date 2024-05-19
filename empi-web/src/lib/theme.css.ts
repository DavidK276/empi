import { createTheme, globalStyle } from '@vanilla-extract/css';

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

globalStyle('a', {
	textDecoration: 'none',
	fontWeight: 700,
	color: vars.link,
	display: 'inline-flex',
	alignItems: 'center',
});

globalStyle('button > a', {
	color: vars.textSecondary,
	padding: `${vars.sm} ${vars.md}`
});

globalStyle('button', {
	display: 'inline-flex',
	alignItems: 'center',
	justifyContent: 'center',
	gap: vars.sm,
	borderRadius: vars.xs,
	padding: `${vars.sm} ${vars.md}`,
	backgroundColor: vars.buttonPrimary,
	color: vars.textSecondary,
	border: 'none',
	whiteSpace: 'nowrap',
	height: 'fit-content',
	fontWeight: 700
});

globalStyle('button[disabled]', {
	backgroundColor: vars.buttonDisabled
});

globalStyle('label', {
	display: 'flex',
	alignItems: 'center'
});

globalStyle('input, textarea', {
	display: 'block',
	marginTop: vars.sm,
	width: '100%',
	borderRadius: vars.xs,
	borderWidth: 0,
	padding: `${vars.xs} ${vars.sm}`,
	marginBottom: vars.lg,
	boxShadow: `0 0 2px ${vars.textPrimary}`
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
	padding: `${vars.xs} ${vars.sm}`,
	border: `1px solid ${vars.textPrimary}`,
	backgroundColor: vars.backgroundPrimary
});

globalStyle('input.error', {
	boxShadow: `0 0 2px ${vars.danger}`,
	marginBottom: 0
});

globalStyle('header', {
	paddingBottom: vars.md
});

globalStyle('footer', {
	marginTop: vars.md,
});

globalStyle('fieldset', {
	margin: `0 0 ${vars.sm} 0`
});

globalStyle('table, th, td', {
	border: `1px solid ${vars.textPrimary}`,
	borderCollapse: 'collapse',
	padding: vars.sm
});

globalStyle('.m-w-full', {
	'@media': {
		'screen and (max-width: 768px)': {
			width: '100% !important'
		}
	}
});