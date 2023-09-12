import React from 'react';
import {
  DataGrid,
  GridColDef,
  GridFilterModel,
  GridFilterItem,
  GridToolbarContainer,
  GridToolbarExport,
} from '@mui/x-data-grid';

type DataField = string | number;

interface DataItem {
  id: number; // DataGrid requires an 'id' field
  [key: string]: DataField;
}

interface DataTableProps {
  data: DataItem[];
  columns: GridColDef[]; // Using GridColDef from DataGrid
}

const csvOptions = {
  delimiter: ',',
};

const ExportToolbar = () => {
  return (
    <GridToolbarContainer>
      <GridToolbarExport csvOptions={csvOptions} />
    </GridToolbarContainer>
  );
};

const DataTable: React.FC<DataTableProps> = ({ data, columns }) => {
  // State for managing filters
  const [filterModel, setFilterModel] = React.useState<GridFilterModel>({
    items: [],
  });

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={data}
        columns={columns.map((col) => ({ ...col, filterable: true }))} // Ensure all columns are filterable
        autoPageSize
        pageSizeOptions={[5, 25, 50, 100]}
        filterModel={filterModel}
        onFilterModelChange={(model) => setFilterModel(model)}
        slots={{ toolbar: ExportToolbar }}
        disableRowSelectionOnClick
      />
    </div>
  );
};

export default DataTable;
