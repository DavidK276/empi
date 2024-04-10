import { globalStyle, style } from '@vanilla-extract/css';
import { vars } from './theme.css';

export const row = style({
	display: 'flex',
	flexDirection: 'row',
	gap: vars.md,
	selectors: {
		'.ver-top&': {
			alignItems: 'top'
		},
		'.ver-center&': {
			alignItems: 'center'
		},
		'.hor-left&': {
			justifyContent: 'start'
		},
		'.hor-center&': {
			justifyContent: 'center'
		}
	}
});

export const col = style({
	display: 'flex',
	flexDirection: 'column',
	gap: vars.md,
	selectors: {
		'.ver-top&': {
			alignItems: 'top'
		},
		'.ver-center&': {
			alignItems: 'center'
		},
		'.hor-left&': {
			justifyContent: 'start'
		},
		'.hor-center&': {
			justifyContent: 'center'
		}
	}
});

export const dropdown = style({
	position: 'relative',
	display: 'inline-block',
	float: 'right',
	'@media': {
		'screen and (min-width: 768px)': {
			float: 'left'
		}
	}
});

export const dropdownContent = style({
	display: 'none',
	position: 'absolute',
	right: 0,
	minWidth: '250px',
	boxShadow: '0px 8px 16px 0px rgba(0,0,0,0.4)',
	backgroundColor: vars.backgroundPrimary,
	zIndex: 1,
	borderRadius: vars.sm,
	paddingLeft: vars.lg,
	paddingRight: vars.lg,
	paddingTop: 0,
	paddingBottom: vars.lg,
	gap: vars.lg,
	selectors: {
		[`${dropdown}:hover &,${dropdown}.show &`]: {
			display: 'flex'
		}
	},
	'@media': {
		'screen and (min-width: 768px)': {
			left: 0
		}
	}
});

export const content = style({
	maxWidth: 1280,
	width: '100%'
});

export const hidden = style({
	display: 'none'
});

export const error = style({
	color: 'red',
	display: 'block',
	margin: '4px 0'
});

export const box = style({
	border: '1px solid gray',
	borderRadius: vars.xs,
	boxShadow: '0 0 4px gray',
	margin: `${vars.sm} 0`,
	padding: `${vars.sm}`
})

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
	border: 'none'
});

globalStyle('button[type="submit"]', {
	marginTop: vars.md
});

globalStyle('button[disabled]', {
	backgroundColor: vars.buttonDisabled
});

globalStyle('label', {
	display: 'flex',
	marginTop: vars.lg,
	color: vars.textTertiary
});

globalStyle('input', {
	display: 'block',
	marginTop: vars.sm,
	width: '100%',
	borderRadius: vars.xs,
	borderWidth: 0,
	padding: `${vars.xs} ${vars.sm}`,
	boxShadow: `0 0 2px gray`,
	boxSizing: 'border-box'
});

globalStyle('select', {
	display: 'block',
	marginTop: vars.sm,
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
	paddingTop: vars.md
});