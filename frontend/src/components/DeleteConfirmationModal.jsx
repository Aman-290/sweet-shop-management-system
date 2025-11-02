const DeleteConfirmationModal = ({ isOpen, onClose, onConfirm, sweetName }) => {
  if (!isOpen) return null

  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4'>
      <div className='bg-white rounded-xl shadow-2xl max-w-md w-full p-6'>
        <h2 className='text-2xl font-bold text-gray-900 mb-4'>Delete Sweet</h2>
        <p className='text-gray-600 mb-6'>
          Are you sure you want to delete <strong>{sweetName}</strong>? This action cannot be undone.
        </p>
        <div className='flex space-x-4'>
          <button onClick={onConfirm} className='btn-danger flex-1'>
            Delete
          </button>
          <button onClick={onClose} className='btn-secondary flex-1'>
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}

export default DeleteConfirmationModal
