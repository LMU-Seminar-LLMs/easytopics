import React, { useRef, useEffect } from 'react';

type ScatterOverlayProps = {
  content: string;
  onClose: () => void;
};

const ScatterOverlay: React.FC<ScatterOverlayProps> = ({
  content,
  onClose,
}) => {
  const modalRef = useRef<HTMLDivElement | null>(null); // create a ref to the modal div

  // this function checks if a click was outside of the modal
  const handleClickOutside = (event: MouseEvent) => {
    if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
      onClose();
    }
  };

  useEffect(() => {
    // attach the listener to the document
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      // clean up the listener when the component unmounts
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className='fixed inset-0 flex items-center justify-center z-50'>
      <div
        ref={modalRef}
        className='bg-white bg-opacity-90 p-8 rounded-lg shadow-md'
      >
        <div className='text-right'>
          <button
            onClick={onClose}
            className='text-gray-500 hover:text-gray-800'
          >
            &times;
          </button>
        </div>
        <div>{content}</div>
      </div>
    </div>
  );
};

export default ScatterOverlay;
