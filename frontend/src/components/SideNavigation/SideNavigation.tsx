import { BottomLinks, TopLinks } from '@/constants'
import { Button, Text } from '@mantine/core'
import { FunctionComponent } from 'react'
import { NavLink } from 'react-router-dom'

interface SideNavigationProps {}

const SideNavigation: FunctionComponent<SideNavigationProps> = () => {
  return (
    <aside className='hidden h-auto flex-col border-r border-gray-100 pt-2 md:flex'>
      <div className='px-4 pb-3 pt-1'>
        {TopLinks.map(link => {
          return (
            <NavLink
              to={link.route}
              key={link.name}
              style={{ display: 'block', marginBottom: '0.75rem' }}
              className={({ isActive }) =>
                [isActive ? 'activeLink' : 'sideLink'].join(' ')
              }
            >
              <Button
                variant='default'
                justify='space-between'
                leftSection={
                  <img src={link.icon} alt='folderIcon' className='h-5 w-5' />
                }
                rightSection={<span />}
                fullWidth
                className='flex w-52 border-none p-2 text-black'
              >
                {link.name}
              </Button>
            </NavLink>
          )
        })}
        <Text className='mt-2 pl-2 text-gray-400'>Библиотека</Text>
        {BottomLinks.map(link => {
          return (
            <NavLink
              to={`${link.route}`}
              key={link.name}
              style={{ display: 'block', marginBottom: '0.75rem' }}
              className={({ isActive }) =>
                [isActive ? 'activeLink' : 'sideLink'].join(' ')
              }
            >
              <Button
                variant='default'
                justify='space-between'
                leftSection={
                  <img src={link.icon} alt='folderIcon' className='h-5 w-5' />
                }
                rightSection={<span />}
                fullWidth
                className='flex w-52 border-none p-2 text-black'
              >
                {link.name}
              </Button>
            </NavLink>
          )
        })}
      </div>
    </aside>
  )
}

export default SideNavigation
