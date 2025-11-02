import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Navbar = () => {
  const { user, logout, isAdmin } = useAuth()
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <nav className='bg-white shadow-md sticky top-0 z-50'>
      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
        <div className='flex justify-between items-center h-16'>
          <div className='flex items-center space-x-8'>
            <h1 className='text-2xl font-bold bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent'>
               Sweet Shop
            </h1>
            <div className='hidden md:flex space-x-4'>
              <Link
                to='/'
                className={`px-3 py-2 rounded-lg font-medium transition-colors ${
                  isActive('/') 
                    ? 'bg-primary-100 text-primary-700' 
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Dashboard
              </Link>
              {isAdmin && (
                <Link
                  to='/admin'
                  className={`px-3 py-2 rounded-lg font-medium transition-colors ${
                    isActive('/admin') 
                      ? 'bg-primary-100 text-primary-700' 
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  Admin
                </Link>
              )}
            </div>
          </div>
          <div className='flex items-center space-x-4'>
            <span className='text-sm text-gray-600 hidden sm:block'>
              {user?.email}
            </span>
            <button
              onClick={logout}
              className='btn-secondary'
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
