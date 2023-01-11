export const styles = (theme) => ({
    cropContainer: {
      position: 'relative',
      width: '100%',
      background: '#333',
      maxHeight: 200,
    },
    cropButton: {
      flexShrink: 0,
      marginLeft: 16,
    },
    controls: {
      padding: 16,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'stretch',
      [theme.breakpoints.up('sm')]: {
        flexDirection: 'row',
        alignItems: 'center',
      },
    },
  })