import { useState, useEffect } from 'react'
import { sweetsAPI } from '../services/api'
import SweetFormModal from '../components/SweetFormModal'
import DeleteConfirmationModal from '../components/DeleteConfirmationModal'
import RestockModal from '../components/RestockModal'
import toast from 'react-hot-toast'

const AdminPage = () => {
  const [sweets, setSweets] = useState([])
  const [loading, setLoading] = useState(true)
  const [formModal, setFormModal] = useState({ isOpen: false, mode: 'create', sweet: null })
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, sweet: null })
  const [restockModal, setRestockModal] = useState({ isOpen: false, sweet: null })

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

  const handleCreate = async (sweetData) => {
    try {
      const newSweet = await sweetsAPI.create(sweetData)
      setSweets([...sweets, newSweet])
      setFormModal({ isOpen: false, mode: 'create', sweet: null })
      toast.success('Sweet created successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create sweet')
    }
  }

  const handleUpdate = async (sweetData) => {
    try {
      const updated = await sweetsAPI.update(formModal.sweet.id, sweetData)
      setSweets(sweets.map(s => s.id === updated.id ? updated : s))
      setFormModal({ isOpen: false, mode: 'create', sweet: null })
      toast.success('Sweet updated successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update sweet')
    }
  }

  const handleDelete = async () => {
    try {
      await sweetsAPI.delete(deleteModal.sweet.id)
      setSweets(sweets.filter(s => s.id !== deleteModal.sweet.id))
      setDeleteModal({ isOpen: false, sweet: null })
      toast.success('Sweet deleted successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to delete sweet')
    }
  }

  const handleRestock = async (quantity) => {
    try {
      const updated = await sweetsAPI.restock(restockModal.sweet.id, quantity)
      setSweets(sweets.map(s => s.id === updated.id ? updated : s))
      setRestockModal({ isOpen: false, sweet: null })
      toast.success('Sweet restocked successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to restock sweet')
    }
  }

  return (
    <div className='min-h-screen py-8 px-4 sm:px-6 lg:px-8'>
      <div className='max-w-7xl mx-auto'>
        <div className='flex justify-between items-center mb-8'>
          <h1 className='text-4xl font-bold text-gray-900'>Admin Management</h1>
          <button
            onClick={() => setFormModal({ isOpen: true, mode: 'create', sweet: null })}
            className='btn-primary'
          >
             Add New Sweet
          </button>
        </div>

        {loading ? (
          <div className='flex justify-center items-center py-12'>
            <div className='animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600'></div>
          </div>
        ) : (
          <div className='card overflow-hidden'>
            <div className='overflow-x-auto'>
              <table className='min-w-full divide-y divide-gray-200'>
                <thead className='bg-gray-50'>
                  <tr>
                    <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Name
                    </th>
                    <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Category
                    </th>
                    <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Price
                    </th>
                    <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Quantity
                    </th>
                    <th className='px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider'>
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className='bg-white divide-y divide-gray-200'>
                  {sweets.map((sweet) => (
                    <tr key={sweet.id} className='hover:bg-gray-50 transition-colors'>
                      <td className='px-6 py-4 whitespace-nowrap'>
                        <div className='text-sm font-medium text-gray-900'>{sweet.name}</div>
                      </td>
                      <td className='px-6 py-4 whitespace-nowrap'>
                        <span className='px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-primary-100 text-primary-800'>
                          {sweet.category}
                        </span>
                      </td>
                      <td className='px-6 py-4 whitespace-nowrap'>
                        <div className='text-sm text-gray-900'></div>
                      </td>
                      <td className='px-6 py-4 whitespace-nowrap'>
                        <div className={`text-sm font-semibold ${sweet.quantity === 0 ? 'text-red-600' : 'text-green-600'}`}>
                          {sweet.quantity}
                        </div>
                      </td>
                      <td className='px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2'>
                        <button
                          onClick={() => setFormModal({ isOpen: true, mode: 'edit', sweet })}
                          className='text-primary-600 hover:text-primary-900 font-semibold'
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => setRestockModal({ isOpen: true, sweet })}
                          className='text-accent-600 hover:text-accent-900 font-semibold'
                        >
                          Restock
                        </button>
                        <button
                          onClick={() => setDeleteModal({ isOpen: true, sweet })}
                          className='text-red-600 hover:text-red-900 font-semibold'
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {sweets.length === 0 && (
              <div className='text-center py-12'>
                <p className='text-gray-500 text-lg'>No sweets yet. Add your first sweet!</p>
              </div>
            )}
          </div>
        )}
      </div>

      <SweetFormModal
        isOpen={formModal.isOpen}
        onClose={() => setFormModal({ isOpen: false, mode: 'create', sweet: null })}
        onSubmit={formModal.mode === 'edit' ? handleUpdate : handleCreate}
        sweet={formModal.sweet}
        mode={formModal.mode}
      />

      <DeleteConfirmationModal
        isOpen={deleteModal.isOpen}
        onClose={() => setDeleteModal({ isOpen: false, sweet: null })}
        onConfirm={handleDelete}
        sweetName={deleteModal.sweet?.name}
      />

      <RestockModal
        isOpen={restockModal.isOpen}
        onClose={() => setRestockModal({ isOpen: false, sweet: null })}
        onSubmit={handleRestock}
        sweet={restockModal.sweet}
      />
    </div>
  )
}

export default AdminPage
