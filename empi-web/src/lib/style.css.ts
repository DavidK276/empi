import { globalStyle, style } from '@vanilla-extract/css';
import { vars } from './theme.css';

export const container = style({
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
	minWidth: '200px',
	boxShadow: '0px 8px 16px 0px rgba(0,0,0,0.4)',
	backgroundColor: vars.backgroundPrimary,
	zIndex: 1,
	borderRadius: vars.sm,
	padding: vars.lg,
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

globalStyle('body', {
	fontFamily: '"Source Sans Pro",sans-serif'
});

globalStyle('a', {
	textDecoration: 'none',
	fontWeight: 700,
	margin: `0 ${vars.sm}`,
	color: vars.link
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
	backgroundColor: 'rgb(37 99 235)',
	color: vars.textSecondary,
	border: 'none'
});

globalStyle('input', {
	borderRadius: vars.xs,
	borderWidth: 0,
	padding: `${vars.xs} ${vars.sm}`,
	boxShadow: `0 0 2px gray`,
});