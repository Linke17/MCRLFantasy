import * as React from 'react';
import Box from '@mui/material/Box';
import { createTheme } from '@mui/material/styles';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import { AppProvider } from '@toolpad/core/AppProvider';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import type { Session, Router, Navigation } from '@toolpad/core';
import PlayerStats from './PlayerStats.tsx';

const PAGES = [
  {
    title: 'Player Stats',
    pathname: '/stats',
    element: <PlayerStats />,
  },
];

const NAVIGATION: Navigation = [
  {
    segment: 'stats',
    title: 'Player Stats',
    icon: <QueryStatsIcon />,

  },
];

const demoTheme = createTheme({
  cssVariables: {
    colorSchemeSelector: 'data-toolpad-color-scheme',
  },
  colorSchemes: { light: true, dark: true },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 600,
      lg: 1200,
      xl: 1536,
    },
  },
});

function PageContent({ pathname }: { pathname: string }) {

  const page = PAGES.find((page) => page.pathname === pathname);
  window.history.replaceState(null, '', pathname);

  return (
    <Box
      sx={{
        py: 4,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center',
      }}
    >
      {page && page.element}
    </Box>
  );
}

interface DemoProps {
  /**
   * Injected by the documentation to work in an iframe.
   * Remove this when copying and pasting into your project.
   */
  window?: () => Window;
}

export default function DashboardLayoutAccount(props: DemoProps) {
  const { window } = props;

  const [session, setSession] = React.useState<Session | null>({
    user: {
      name: 'Ryan Kruk',
      email: 'ryankruk2003@gmail.com',
      image: 'https://fohn.net/duck-pictures-facts/mallard-duck-1024-768.jpg',
    },
  });

  const authentication = React.useMemo(() => {
    return {
      signIn: () => {
        setSession({
          user: {
            name: 'Ryan Kruk',
            email: 'ryankruk2003@gmail.com',
            image: 'https://fohn.net/duck-pictures-facts/mallard-duck-1024-768.jpg',
          },
        });
      },
      signOut: () => {
        setSession(null);
      },
    };
  }, []);

  const [pathname, setPathname] = React.useState('/');

  const router = React.useMemo<Router>(() => {
    return {
      pathname,
      searchParams: new URLSearchParams(),
      navigate: (path) => setPathname(String(path)),
    };
  }, [pathname]);

  // Remove this const when copying and pasting into your project.
  const demoWindow = window !== undefined ? window() : undefined;

  return (
    // preview-start
    <AppProvider
      session={session}
      authentication={authentication}
      navigation={NAVIGATION}
      branding={{
        logo: <img src="https://logos-world.net/wp-content/uploads/2020/11/Rocket-League-Emblem.png" alt="MUI logo" />,
        title: 'Midwest Fuckery',
      }}
      router={router}
      theme={demoTheme}
      window={demoWindow}
    >
      <DashboardLayout>
        <PageContent pathname={pathname} />
      </DashboardLayout>
    </AppProvider>
    // preview-end
  );
}