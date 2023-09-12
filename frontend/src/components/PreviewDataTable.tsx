import React, { useState } from 'react';

interface DataItem {
  id: number;
  text: string;
}

interface DataTableProps {
  data: DataItem[];
}

const DataTable: React.FC<DataTableProps> = ({ data }) => {
  const [searchText, setSearchText] = useState('');
  const [searchTextById, setSearchTextById] = useState('');
  const [searchTextByText, setSearchTextByText] = useState('');

  const filteredData = data.filter((item) => {
    const idMatch = item.id.toString().includes(searchTextById);
    const textMatch = item.text.includes(searchTextByText);

    return idMatch && textMatch;
  });

  return (
    <div className='relative'>
      <div className='mb-4 flex space-x-4'>
        <input
          className='w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:outline-none focus:ring focus:border-blue-300'
          type='text'
          placeholder='Search...'
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        />
      </div>
      <div className='max-h-[400px] overflow-y-auto'>
        <table className='min-w-full divide-y divide-gray-200'>
          <thead className='sticky top-0 bg-gray-100'>
            <tr>
              <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-[1px]'>
                ID
                <input
                  className='w-full border border-gray-300 rounded-md shadow-sm px-2 py-1 focus:outline-none focus:ring focus:border-blue-300'
                  type='text'
                  placeholder='Search ID...'
                  value={searchTextById}
                  onChange={(e) => setSearchTextById(e.target.value)}
                />
              </th>
              <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-auto'>
                Text
                <input
                  className='w-full border border-gray-300 rounded-md shadow-sm px-2 py-1 focus:outline-none focus:ring focus:border-blue-300'
                  type='text'
                  placeholder='Search Text...'
                  value={searchTextByText}
                  onChange={(e) => setSearchTextByText(e.target.value)}
                />
              </th>
            </tr>
          </thead>
          <tbody className='bg-white divide-y divide-gray-200'>
            {filteredData.map((item) => (
              <tr key={item.id}>
                <td className='px-6 py-4 whitespace-nowrap'>{item.id}</td>
                <td className='px-6 py-4 whitespace-nowrap'>{item.text}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;
