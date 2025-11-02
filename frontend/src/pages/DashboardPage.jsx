import { useState, useEffect } from 'react'
import { sweetsAPI } from '../services/api'
import SweetCard from '../components/SweetCard'
import toast from 'react-hot-toast'

const DashboardPage = () => {
  const [sweets, setSweets] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchParams, setSearchParams] = useState({
    name: '',
    category: '',
    min_price: '',
    max_price: '',
  })

  useEffect(() => {
    fetchSweets()
  }, [])

  const fetchSweets = async () => {
    setLoading(true)
    try {
      const data = await sweetsAPI.getAll()
      setSweets(data)
    } catch (error) {
      toast.error('Failed to load sweets')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const params = {}
      if (searchParams.name) params.name = searchParams.name
      if (searchParams.category) params.category = searchParams.category
      if (searchParams.min_price) params.min_price = parseFloat(searchParams.min_price)
      if (searchParams.max_price) params.max_price = parseFloat(searchParams.max_price)
      
      const data = await sweetsAPI.search(params)
      setSweets(data)
    } catch (error) {
      toast.error('Search failed')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSearchParams({ name: '', category: '', min_price: '', max_price: '' })
    fetchSweets()
  }

  const handleSweetUpdate = (updatedSweet) => {
    setSweets(sweets.map(s => s.id === updatedSweet.id ? updatedSweet : s))
  }

  return (
    <div className='min-h-screen py-8 px-4 sm:px-6 lg:px-8'>
      <div className='max-w-7xl mx-auto'>
        <h1 className='text-4xl font-bold text-gray-900 mb-8'>Sweet Collection</h1>
        
        {/* Search/Filter Section */}
        <div className='card p-6 mb-8'>
          <form onSubmit={handleSearch} className='space-y-4'>
            <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-2'>
                  Sweet Name
                </label>
                <input
                  type='text'
                  value={searchParams.name}
                  onChange={(e) => setSearchParams({ ...searchParams, name: e.target.value })}
                  className='input-field'
                  placeholder='Search by name...'
                />
              </div>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-2'>
                  Category
                </label>
                <input
                  type='text'
                  value={searchParams.category}
                  onChange={(e) => setSearchParams({ ...searchParams, category: e.target.value })}
                  className='input-field'
                  placeholder='e.g., Chocolate'
                />
              </div>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-2'>
                  Min Price
                </label>
                <input
                  type='number'
                  step='0.01'
                  value={searchParams.min_price}
                  onChange={(e) => setSearchParams({ ...searchParams, min_price: e.target.value })}
                  className='input-field'
                  placeholder='0.00'
                />
              </div>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-2'>
                  Max Price
                </label>
                <input
                  type='number'
                  step='0.01'
                  value={searchParams.max_price}
                  onChange={(e) => setSearchParams({ ...searchParams, max_price: e.target.value })}
                  className='input-field'
                  placeholder='100.00'
                />
              </div>
            </div>
            <div className='flex space-x-4'>
              <button type='submit' className='btn-primary'>
                 Search
              </button>
              <button type='button' onClick={handleReset} className='btn-secondary'>
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* Sweets Grid */}
        {loading ? (
          <div className='flex justify-center items-center py-12'>
            <div className='animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600'></div>
          </div>
        ) : sweets.length === 0 ? (
          <div className='text-center py-12'>
            <p className='text-gray-500 text-lg'>No sweets found. Try adjusting your search.</p>
          </div>
        ) : (
          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'>
            {sweets.map((sweet) => (
              <SweetCard key={sweet.id} sweet={sweet} onUpdate={handleSweetUpdate} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default DashboardPage
