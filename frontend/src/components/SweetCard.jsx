import { useState } from 'react'
import { sweetsAPI } from '../services/api'
import toast from 'react-hot-toast'

const SweetCard = ({ sweet, onUpdate }) => {
  const [purchasing, setPurchasing] = useState(false)

  const handlePurchase = async () => {
    setPurchasing(true)
    try {
      const updated = await sweetsAPI.purchase(sweet.id)
      toast.success('Purchased!')
      onUpdate(updated)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Purchase failed')
    } finally {
      setPurchasing(false)
    }
  }

  const isOutOfStock = sweet.quantity === 0

  return (
    <div className='card p-6 flex flex-col'>
      <div className='flex-1'>
        <div className='flex justify-between items-start mb-3'>
          <h3 className='text-xl font-bold text-gray-900'>{sweet.name}</h3>
          <span className='px-3 py-1 bg-primary-100 text-primary-700 text-sm font-medium rounded-full'>
            {sweet.category}
          </span>
        </div>
        <div className='flex items-baseline space-x-2 mb-4'>
          <span className='text-3xl font-bold text-primary-600'></span>
        </div>
        <div className='flex items-center space-x-2 mb-4'>
          <span className='text-sm font-medium text-gray-600'>Stock:</span>
          <span className={`text-sm font-bold ${isOutOfStock ? 'text-red-600' : 'text-green-600'}`}>
            {sweet.quantity} available
          </span>
        </div>
      </div>
      <button
        onClick={handlePurchase}
        disabled={isOutOfStock || purchasing}
        className='btn-primary w-full'
      >
        {purchasing ? 'Purchasing...' : isOutOfStock ? 'Out of Stock' : 'Purchase'}
      </button>
    </div>
  )
}

export default SweetCard
