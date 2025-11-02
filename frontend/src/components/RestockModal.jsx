import { useState } from 'react'

const RestockModal = ({ isOpen, onClose, onSubmit, sweet }) => {
  const [quantity, setQuantity] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (parseInt(quantity) <= 0) return
    setLoading(true)
    await onSubmit(parseInt(quantity))
    setLoading(false)
    setQuantity('')
  }

  if (!isOpen) return null

  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4'>
      <div className='bg-white rounded-xl shadow-2xl max-w-md w-full p-6'>
        <h2 className='text-2xl font-bold text-gray-900 mb-4'>
          Restock: {sweet?.name}
        </h2>
        <p className='text-gray-600 mb-4'>
          Current stock: <strong>{sweet?.quantity}</strong>
        </p>
        <form onSubmit={handleSubmit} className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Quantity to Add
            </label>
            <input
              type='number'
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              className='input-field'
              required
              min='1'
              placeholder='Enter quantity...'
            />
          </div>
          <div className='flex space-x-4 pt-4'>
            <button
              type='submit'
              disabled={loading}
              className='btn-primary flex-1'
            >
              {loading ? 'Restocking...' : 'Restock'}
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

export default RestockModal
