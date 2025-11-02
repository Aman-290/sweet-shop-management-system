import { useState, useEffect } from 'react'

const SweetFormModal = ({ isOpen, onClose, onSubmit, sweet, mode }) => {
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    price: '',
    quantity: '',
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (sweet && mode === 'edit') {
      setFormData({
        name: sweet.name,
        category: sweet.category,
        price: sweet.price.toString(),
        quantity: sweet.quantity.toString(),
      })
    } else {
      setFormData({ name: '', category: '', price: '', quantity: '' })
    }
  }, [sweet, mode, isOpen])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    await onSubmit({
      ...formData,
      price: parseFloat(formData.price),
      quantity: parseInt(formData.quantity),
    })
    setLoading(false)
  }

  if (!isOpen) return null

  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4'>
      <div className='bg-white rounded-xl shadow-2xl max-w-md w-full p-6'>
        <h2 className='text-2xl font-bold text-gray-900 mb-6'>
          {mode === 'edit' ? 'Edit Sweet' : 'Add New Sweet'}
        </h2>
        <form onSubmit={handleSubmit} className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Name
            </label>
            <input
              type='text'
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className='input-field'
              required
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Category
            </label>
            <input
              type='text'
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className='input-field'
              required
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Price ($)
            </label>
            <input
              type='number'
              step='0.01'
              value={formData.price}
              onChange={(e) => setFormData({ ...formData, price: e.target.value })}
              className='input-field'
              required
              min='0'
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Quantity
            </label>
            <input
              type='number'
              value={formData.quantity}
              onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
              className='input-field'
              required
              min='0'
            />
          </div>
          <div className='flex space-x-4 pt-4'>
            <button
              type='submit'
              disabled={loading}
              className='btn-primary flex-1'
            >
              {loading ? 'Saving...' : mode === 'edit' ? 'Update' : 'Create'}
            </button>
            <button
              type='button'
              onClick={onClose}
              className='btn-secondary flex-1'
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SweetFormModal
