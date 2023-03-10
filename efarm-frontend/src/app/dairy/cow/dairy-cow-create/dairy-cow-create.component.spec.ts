import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyCowCreateComponent } from './dairy-cow-create.component';

describe('DairyCowCreateComponent', () => {
  let component: DairyCowCreateComponent;
  let fixture: ComponentFixture<DairyCowCreateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyCowCreateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyCowCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
