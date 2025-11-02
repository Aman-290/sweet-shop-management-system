import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'

const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    const result = await login(email, password)
    
    if (result.success) {
      toast.success('Welcome back!')
      navigate('/')
    } else {
      toast.error(result.error)
    }
    
    setLoading(false)
  }

  return (
    <div className='min-h-screen flex items-center justify-center px-4 py-12'>
      <div className='max-w-md w-full'>
        <div className='text-center mb-8'>
          <h1 className='text-5xl font-bold bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent mb-3'>
             Sweet Shop
          </h1>
          <p className='text-gray-600 text-lg'>Sign in to your account</p>
        </div>

        <div className='card p-8'>
          <form onSubmit={handleSubmit} className='space-y-6'>
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Email Address
              </label>
              <input
                type='email'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className='input-field'
                placeholder='you@example.com'
                required
              />
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Password
              </label>
              <input
                type='password'
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className='input-field'
                placeholder=''
                required
                minLength={6}
              />
            </div>

            <button
              type='submit'
              disabled={loading}
              className='btn-primary w-full'
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className='mt-6 text-center'>
            <p className='text-sm text-gray-600'>
              Don't have an account?{' '}
              <Link to='/register' className='text-primary-600 hover:text-primary-700 font-medium'>
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
