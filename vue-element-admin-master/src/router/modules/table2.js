/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/views/layout/Layout'

const tableRouter = {
  path: '/complex-table2',
  component: Layout,
  redirect: '/table/complex-table2',
  name: 'Table',
  meta: {
    title: 'Table',
    icon: 'chart'
  },
  children: [
    // {
    //   path: 'dynamic-table',
    //   component: () => import('@/views/table/dynamicTable/index'),
    //   name: 'DynamicTable',
    //   meta: {
    //     title: 'dynamicTable'
    //   }
    // },
    // {
    //   path: 'drag-table',
    //   component: () => import('@/views/table/dragTable'),
    //   name: 'DragTable',
    //   meta: { title: 'dragTable' }
    // },
    // {
    //   path: 'inline-edit-table',
    //   component: () => import('@/views/table/inlineEditTable'),
    //   name: 'InlineEditTable',
    //   meta: {
    //     title: 'inlineEditTable'
    //   }
    // },
    {
      path: 'complex-table2',
      component: () => import('@/views/table/complexTable2'),
      name: 'ComplexTable2',
      meta: {
        title: '限号违章'
      }
    }
  ]
}

export default tableRouter
